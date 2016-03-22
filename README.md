# format-ci
A CI server for verification of autoformatting adherence.

A working server is running [here](http://format-ci.nabijaczleweli.xyz:1082). Should you wish to have any programs installed for verification, please fire an issue.

## Configurability
Environment variables:
  * `GH_TOKEN` -- GitHub OAuth token to use for GH API interaction,
  * `PORT` -- port to listen on. Default: `1082`,
  * `PAYLOAD_URL` -- URL to specify in webhook reference table. Default: `[homepage address]/github_callback`.
