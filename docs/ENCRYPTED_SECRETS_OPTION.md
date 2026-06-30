# Encrypted Secrets Option

The default workflow uses a plaintext local file:

```text
secrets/api_keys.local.env
```

That file is gitignored and should never be committed.

For stronger local security, store the values in a password manager or encrypted archive and copy them into `secrets/api_keys.local.env` only when uploading.

The VPS still needs a readable runtime file at:

```text
/root/devin-investment-os/.env
```

The upload script sets that file to `chmod 600`.
