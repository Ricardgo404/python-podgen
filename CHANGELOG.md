# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [1.1.0] - 2020-03-06
### Added

- Support for the [new Apple Podcast categories][category-new-2019] that were [added August 9th 2019][category-published-2019].
- Documentation of the Warning classes defined by PodGen.

[category-new-2019]: https://podnews.net/article/apple-changed-podcast-categories-2019
[category-published-2019]: https://itunespartner.apple.com/podcasts/whats-new/100002598

### Changed

- Using one of the old iTunes (sub)categories will now generate a `LegacyCategoryWarning`.

### Deprecated

- Importing `NotSupportedByItunesWarning` from `podgen.not_supported_by_itunes_warning`. Import from `podgen` instead.


## [1.0.1] - 2019-10-12
### Added

- This `CHANGELOG.md` file, for documenting notable changes.
- Documentation page about PodGen's roadmap (under Background).

### Changed

- Organization of the documentation, along with other documentation
  improvements and updates.

### Removed

- Support for Python 3.3, due to its age and lack of support.

### Fixed

- `UnicodeEncodeError` when writing a podcast with non-ASCII characters to file
  in an environment where Python defaults to ASCII encoding.
- Incompatibility with unicode strings on Python 2.7.


## [1.0.0] - 2017-05-24
### Added

- The Podcast and Episode classes for easily generating a podcast out of data,
  and related utilities and classes.

[Unreleased]: https://github.com/tobinus/python-podgen/compare/v1.1.0...develop
[1.1.0]: https://github.com/tobinus/python-podgen/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/tobinus/python-podgen/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/tobinus/python-podgen/compare/290045ac...v1.0.0
