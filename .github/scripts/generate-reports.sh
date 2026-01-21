#!/bin/bash
# Generate Allure and coverage reports for GitHub Pages

set -euo pipefail

mkdir -p site

# Generate embedded report
if [ -d "allure-results-embedded" ] && [ "$(ls -A allure-results-embedded 2>/dev/null)" ]; then
  allure generate allure-results-embedded --clean -o site/embedded
else
  mkdir -p site/embedded
  echo "<h1>No embedded test results available</h1>" > site/embedded/index.html
fi

# Generate remote report
if [ -d "allure-results-remote" ] && [ "$(ls -A allure-results-remote 2>/dev/null)" ]; then
  allure generate allure-results-remote --clean -o site/remote
else
  mkdir -p site/remote
  echo "<h1>No remote test results available</h1>" > site/remote/index.html
fi

# Copy coverage report
if [ -d "coverage-report" ] && [ "$(ls -A coverage-report 2>/dev/null)" ]; then
  cp -r coverage-report site/coverage
else
  mkdir -p site/coverage
  echo "<h1>No coverage report available</h1>" > site/coverage/index.html
fi

# Create index page with links to all reports
cp .github/pages/allure-index.html site/index.html

echo "✅ Reports generated successfully"
