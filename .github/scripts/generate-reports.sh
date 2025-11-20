#!/bin/bash
# Generate Allure and coverage reports for GitHub Pages

set -euo pipefail

mkdir -p gh-pages

# Generate embedded report
if [ -d "allure-results-embedded" ] && [ "$(ls -A allure-results-embedded 2>/dev/null)" ]; then
  allure generate allure-results-embedded --clean -o gh-pages/embedded
else
  mkdir -p gh-pages/embedded
  echo "<h1>No embedded test results available</h1>" > gh-pages/embedded/index.html
fi

# Generate remote report
if [ -d "allure-results-remote" ] && [ "$(ls -A allure-results-remote 2>/dev/null)" ]; then
  allure generate allure-results-remote --clean -o gh-pages/remote
else
  mkdir -p gh-pages/remote
  echo "<h1>No remote test results available</h1>" > gh-pages/remote/index.html
fi

# Copy coverage report
if [ -d "coverage-report" ] && [ "$(ls -A coverage-report 2>/dev/null)" ]; then
  cp -r coverage-report gh-pages/coverage
else
  mkdir -p gh-pages/coverage
  echo "<h1>No coverage report available</h1>" > gh-pages/coverage/index.html
fi

# Create index page with links to all reports
cp .github/pages/allure-index.html gh-pages/index.html

echo "✅ Reports generated successfully"
