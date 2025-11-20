## GitHub Actions Workflow

The GitHub Actions workflow automates the testing process using **Dogtail** for E2E GUI automation and **pytest** for unit tests. It also runs code quality checks and publishes test reports to GitHub Pages.

### Automated Execution

The workflow runs automatically on:

- Code pushes to the `master` branch
- Pull requests to `master`
- Manual trigger via `workflow_dispatch`

**Workflow file location**: [`.github/workflows/tests.yml`](/.github/workflows/tests.yml)

### Test Execution

The workflow performs the following checks:

1. **Unit Tests**: Fast, isolated tests for components and business logic
2. **E2E Tests**: GUI automation tests using Dogtail (AT-SPI) on actual AppImage build
3. **Code Quality**: Code quality checks for formatting, type checking, and spell checking
4. **Coverage**: HTML coverage reports generated and published
5. **Allure Reports**: Detailed test execution reports

### Required Secrets

The workflow requires the following secrets (configured in repository settings):

- `CLIENT_ID`: Google OAuth 2.0 Client ID
- `PROJECT_ID`: Google Cloud Project ID
- `CLIENT_SECRET`: Google OAuth 2.0 Client Secret
- `BACKUP_EMAIL_ID`: Google email to be used for the backup operation
- `BACKUP_EMAIL_PASSWORD`: password of the aforementioned Google account
- `GOOGLE_AUTHENTICATOR`: The setup key for Google 2-Factor Authentication (2FA)

> [!NOTE]
>
> - Provide `GOOGLE_AUTHENTICATOR` value **without spaces**
> - Use single quotes around `BACKUP_EMAIL_PASSWORD` and avoid passwords containing single quotes

### Test Reports

After each workflow run, the following reports are published to GitHub Pages:

- **Allure Reports**: Detailed test execution reports with screenshots
  - Embedded mode: `https://<username>.github.io/<repo>/embedded/`
  - Remote mode: `https://<username>.github.io/<repo>/remote/`
- **Coverage Reports**: Code coverage showing which parts are tested at `https://<username>.github.io/<repo>/coverage/`
