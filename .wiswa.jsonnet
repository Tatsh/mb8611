local utils = import 'utils.libjsonnet';

local utils = import 'utils.libjsonnet';

(import 'defaults.libjsonnet') + {
  // Project-specific
  description: 'CLI tool for managing the Motorola MB8611 series modem and maybe other Motorola devices.',
  keywords: ['command line'],
  project_name: 'mb8611',
  version: '0.0.1',
  want_main: true,
  citation+: {
    'date-released': '2025-04-16',
  },
  pyproject+: {
    project+: {
      classifiers+: [
        'Development Status :: 4 - Beta',
      ],
    },
    tool+: {
      poetry+: {
        dependencies+: {
          click: '^8.1.8',
          requests: '^2.32.3',
        },
        group+: {
          dev+: {
            dependencies+: {
              'types-requests': '^2.32.0.20250328',
            },
          },
          tests+: {
            dependencies+: {
                'requests-mock': '^1.12.1'
            }
          }
        },
      },
    },
  },
  // Common
  authors: [
    {
      'family-names': 'Udvare',
      'given-names': 'Andrew',
      email: 'audvare@gmail.com',
      name: '%s %s' % [self['given-names'], self['family-names']],
    },
  ],
  local funding_name = '%s2' % std.asciiLower(self.github_username),
  github_username: 'Tatsh',
  github+: {
    funding+: {
      ko_fi: funding_name,
      liberapay: funding_name,
      patreon: funding_name,
    },
  },
}
