# hypervel-packages-ci

Actions the `ipsocode/hypervel-*` packages share, used as steps in a package's own jobs:

```yaml
- uses: ipsocode/hypervel-packages-ci/conventions@<sha> # v1
- uses: ipsocode/hypervel-packages-ci/install@<sha> # v1
  with:
    php: '8.4'
- uses: ipsocode/hypervel-packages-ci/suite@<sha> # v1
  with:
    php: '8.4'
    style: 'true'
    min-coverage: '100'
```

| Action | Does |
|---|---|
| `conventions` | Checks the calling checkout against the packages' conventions. |
| `install` | Installs a package's dependencies with Composer, with Composer's and the tools' caches (`tests/.cache`). |
| `suite` | Runs php-cs-fixer, PHPStan and the test suite, under the coverage gate when `min-coverage` is set. |

A package keeps its jobs, containers and triggers; only the steps live here. Pin `uses:` to a full
commit SHA, as the packages' Actions policy requires.

## License

[MIT](LICENSE).
