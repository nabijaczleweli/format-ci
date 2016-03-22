# format-ci
A CI server for verification of autoformatting adherence.

A working server is running [here](http://format-ci.nabijaczleweli.xyz:1082). Should you wish to have any programs installed for verification, please fire an issue.

## Configurability
Environment variables:
  * `GH_TOKEN` -- GitHub OAuth token to use for GH API interaction,
  * `OWN_URL` -- the URL by which one can reach the home page, e.g. `http://format-ci.nabijaczleweli.xyz:1082`,
  * `GMAIL_USERNAME`<sub>opt</sub> -- username used for GMail authentication, required if e-mails are to be sent,
  * `GMAIL_PASSWORD`<sub>opt</sub> -- password used for GMail authentication, required if e-mails are to be sent,
  * `PORT`<sub>opt</sub> -- port to listen on. Default: `1082`,
  * `PAYLOAD_URL`<sub>opt</sub> -- URL to specify in webhook reference table. Default: `$OWN_URL/github_callback`.
