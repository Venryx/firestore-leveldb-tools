# firestore-leveldb-tools

Documentation and tools for reading/converting Firestore gcloud (LevelDB) backups.

### Setup

1) Make sure Python 2.7 is installed, and present in your "PATH" environment variable. (or just supply the absolute path to its `python` executable in usage step 1)
2) Clone/download this repo to disk.

### Usage

1) Run `python ToJSON.py PATH_TO_FIRESTORE_BACKUP_FOLDER` (pass the direct parent folder of the "output-0", etc. files)
2) A `Data.json` file will be created in the backup folder, containing an array of entries. Each entry is a document within one of the collections; the source collection must be inferred from the data shape for now.

### SDK Dependencies

The `ToJSON.py` script relies on some scripts within the google-cloud-sdk and appengine-sdk. A stripped-down version of each of these is included in this repo for convenience; however, if you need to use a different version of these sdks for some reason, you can download other versions from here:
* Google Cloud SDK archive (included: `google-cloud-sdk-180.0.1-windows-x86_64.zip`): https://console.cloud.google.com/storage/browser/cloud-sdk-release
* AppEngine SDK archive (included: `180/google_appengine_1.8.0.zip`): https://console.cloud.google.com/storage/browser/appengine-sdks/deprecated

To use the alternate version downloaded, extract the archives, then replace the corresponding contents within the `SDKs` folder.