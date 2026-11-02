# hypervel-packages-ci

What the `ipsocode/hypervel-*` packages share in CI, as steps and as a reusable workflow. A package keeps
its own jobs, containers and triggers; only the steps live here.

Each folder is named after the package workflow it serves, in that workflow's spelling (`initial`, `tests`,
`branches`, `publish`, `pages`, `databases`).

```yaml
- uses: ipsocode/hypervel-packages-ci/initial/conventions@<sha> # v1
- uses: ipsocode/hypervel-packages-ci/tests/install@<sha> # v1
  with:
    php: '8.4'
- uses: ipsocode/hypervel-packages-ci/tests/suite@<sha> # v1
  with:
    php: '8.4'
    style: 'true'
    min-coverage: '100'
```

| Action | Does | The calling job needs |
|---|---|---|
| `initial/conventions` | Checks the calling checkout against the packages' conventions. | `contents: read` |
| `tests/install` | Installs a package's dependencies with Composer, with Composer's and the tools' caches (`tests/.cache`). | `contents: read` |
| `tests/suite` | Runs php-cs-fixer, PHPStan and the test suite, under the coverage gate when `min-coverage` is set. | `contents: read` |
| `branches/feature` | Creates a feature issue's linked `feature/<n>-<slug>` branch and writes its `Base branch:` line. | `contents: write`, `issues: write` |
| `publish/plan` | Decides the version, the tag and whether anything ships. | `contents: read`, `pull-requests: read` |
| `publish/release` | Writes the release notes, tags the planned commit and publishes the release, in that order. | `contents: write`, `pull-requests: read` |
| `pages/build` | Builds `src/docs/` into a Pages artifact. Deploying stays in the package. | `contents: read`, `pages: read` |

`publish/plan` and `publish/release` need the repository checked out first, with `fetch-depth: 0` and
`fetch-tags: true`; `publish/release` also needs the planned commit and the checkout's credentials.

## Reusable workflow

`databases` runs a package's suite against MySQL, MariaDB, PostgreSQL and SQLite on each PHP version:

```yaml
jobs:
  databases:
    uses: ipsocode/hypervel-packages-ci/.github/workflows/databases.yml@<sha> # v1
```

Inputs: `php`, a JSON array (default `["8.4", "8.5"]`), and `script`, the package's script that runs the suite
against one connection (default `bin/run-database-tests.sh`). The package's `testbench.yaml` sets
`OTEL_SDK_DISABLED: true` under `env:`; `phpunit.xml` cannot, because PHPUnit turns `true` into `1`, which the
OpenTelemetry SDK rejects.

## Pinning

Pin `uses:` to a full commit SHA, as the packages' Actions policy requires. A workflow here that uses an action
here pins an earlier commit, so a bump lands one change behind.

## License

[MIT](LICENSE).
