#!/usr/bin/env bash

set -e  # Exit on error
set -o pipefail  # Exit if any command in a pipeline fails
set -u  # Treat unset variables as errors

# Define paths
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
E2E_DIR="$ROOT_DIR/e2e_tests"
TESTS_DIR="$E2E_DIR/test/spec"
APPLICATIONS_DIR="$E2E_DIR/applications"
VERSION=$(grep '__version__' ./src/version.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)
APP1_NAME=$(grep '^APP1_NAME' accessible_constant.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)
APP2_NAME=$(grep '^APP2_NAME' accessible_constant.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)

# Paths for the built applications
FIRST_WALLET_NAME="iriswallet_${APP1_NAME}-${VERSION}-x86_64.AppImage"
SECOND_WALLET_NAME="iriswallet_${APP2_NAME}-${VERSION}-x86_64.AppImage"

APP1_PATH="$APPLICATIONS_DIR/$FIRST_WALLET_NAME"
APP2_PATH="$APPLICATIONS_DIR/$SECOND_WALLET_NAME"

# Paths for constants file
CONSTANT_FILE="./src/utils/constant.py"
BACKUP_FILE="./src/utils/constant_backup.py"

# Command-line arguments
TEST_FILE=""
RUN_ALL=false
FORCE_BUILD=false
WALLET_MODES=()

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --force-build)
            FORCE_BUILD=true
            shift
            ;;
        --all)
            RUN_ALL=true
            shift
            ;;
        --wallet-mode)
            if [[ -n "$2" ]]; then
                WALLET_MODES+=("$2")
                shift 2
            else
                echo "Error: --wallet-mode requires a value (embedded or remote)."
                exit 1
            fi
            ;;
        *)
            TEST_FILE=$1
            shift
            ;;
    esac
done

# Default to both wallet modes if none are specified
if [[ ${#WALLET_MODES[@]} -eq 0 ]]; then
    WALLET_MODES=("embedded" "remote")
fi

# Ensure constants are restored if the script exits unexpectedly
trap restore_constants EXIT

# Function to temporarily modify constants before build
modify_constants() {
    echo "Modifying constants for testing..."
    [[ ! -f "$BACKUP_FILE" ]] && cp "$CONSTANT_FILE" "$BACKUP_FILE"

    sed -i -E "
        s|BITCOIND_RPC_HOST_REGTEST = 'regtest-bitcoind.rgbtools.org'|BITCOIND_RPC_HOST_REGTEST = 'localhost'|;
        s|BITCOIND_RPC_PORT_REGTEST = 80|BITCOIND_RPC_PORT_REGTEST = 18443|;
        s|INDEXER_URL_REGTEST = 'electrum.rgbtools.org:50041'|INDEXER_URL_REGTEST = '127.0.0.1:50001'|;
        s|PROXY_ENDPOINT_REGTEST = 'rpcs://proxy.iriswallet.com/0.2/json-rpc'|PROXY_ENDPOINT_REGTEST = 'rpc://127.0.0.1:3000/json-rpc'|;
    " "$CONSTANT_FILE"

    echo "Constants modified."
}

# Function to restore original constants after build
restore_constants() {
    if [[ -f "$BACKUP_FILE" ]]; then
        echo "Restoring original constants..."
        mv -f "$BACKUP_FILE" "$CONSTANT_FILE"
        echo "Original constants restored."
    fi
}

# Function to move an application after it is built
move_application() {
    local app_name=$1
    local app_path="$ROOT_DIR/$app_name"

    echo "Moving $app_name to $APPLICATIONS_DIR..."
    mkdir -p "$APPLICATIONS_DIR"

    if [[ -f "$app_path" ]]; then
        mv -f "$app_path" "$APPLICATIONS_DIR/"
        echo "$app_name moved successfully."
    else
        echo "Error: $app_name not found at $app_path"
        exit 1
    fi
}

# Function to build applications if they are missing
build_applications() {
    echo "Building applications..."

    cd "$ROOT_DIR" || exit 1

    # Modify constants before build
    modify_constants

    echo "Building first wallet..."
    build-iris-wallet --network regtest --distribution appimage --app-name "${APP1_NAME}" &
    wait $!
    move_application "$FIRST_WALLET_NAME"

    echo "Building second wallet..."
    build-iris-wallet --network regtest --distribution appimage --app-name "${APP2_NAME}" &
    wait $!
    move_application "$SECOND_WALLET_NAME"

    echo "Build process completed."
}

# Populate TEST_FILES array with all test files
TEST_FILES=()
while IFS= read -r -d '' file; do
    TEST_FILES+=("$file")
done < <(find "$TESTS_DIR" -name "test_*.py" -print0 | sort -z)

ensure_applications_exist() {
    if [[ "$FORCE_BUILD" == true ]]; then
        echo "--force-build flag detected. Rebuilding applications..."
        build_applications
        exit 0
    fi

    if [[ ! -f "$APP1_PATH" || ! -f "$APP2_PATH" ]]; then
        echo "One or both applications are missing. Initiating build..."
        build_applications
    else
        echo "Both applications are available. Proceeding with tests."
    fi
}

# Helper function to print test suite header
print_test_header() {
    local test_name=$1
    local test_path=$2
    local wallet_mode=$3

    echo "========================================"
    echo "Test Suite: $test_name"
    echo "Path      : $test_path"
    echo "Mode      : $wallet_mode"
    echo "========================================"
}

# Helper function to print failure message
print_failure() {
    local test_name=$1
    local wallet_mode=$2

    echo ""
    echo "✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗"
    echo "✗ FAILED: $test_name in ${wallet_mode^^} mode"
    echo "✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗"
    echo ""
}

# Helper function to print summary failure message
print_summary_failure() {
    local wallet_mode=$1

    echo ""
    echo "════════════════════════════════════════"
    echo "One or more test suites FAILED in ${wallet_mode^^} mode"
    echo "════════════════════════════════════════"
}

run_e2e_tests() {
    local wallet_mode=$1
    local results_dir="allure-results-${wallet_mode}"
    local EXIT_CODE=0

    echo "Running E2E tests with wallet mode: $wallet_mode"

    rm -rf "$results_dir"
    mkdir -p "$results_dir"

    if [[ "$RUN_ALL" == true ]]; then
        echo "Running full test suite (per-file)..."
        for test_file in "${TEST_FILES[@]}"; do
            print_test_header "$(basename "$test_file")" "$test_file" "$wallet_mode"
            if ! pytest -s "$test_file" --alluredir="$results_dir" --wallet-mode "$wallet_mode"; then
                print_failure "$(basename "$test_file")" "$wallet_mode"
                EXIT_CODE=1
            fi
        done

        if [[ $EXIT_CODE -ne 0 ]]; then
            print_summary_failure "$wallet_mode"
            exit $EXIT_CODE
        fi
    elif [[ -n "$TEST_FILE" ]]; then
        print_test_header "$TEST_FILE" "$TESTS_DIR/$TEST_FILE" "$wallet_mode"
        if ! pytest -s "$TESTS_DIR/$TEST_FILE" --alluredir="$results_dir" --wallet-mode "$wallet_mode"; then
            print_failure "$TEST_FILE" "$wallet_mode"
            exit 1
        fi
    else
        echo "No test file provided. Use --all to run all tests."
        exit 1
    fi
}

ensure_applications_exist

for mode in "${WALLET_MODES[@]}"; do
    run_e2e_tests "$mode"
done

echo "Setup and tests completed successfully!"
