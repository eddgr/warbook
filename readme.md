# Warbook
A command line work journal

# Requirements
- Python 3
- S3 account if you plan to sync

# Getting Started
- Create `env_vars.sh` if you plan to sync output files to S3. Template:

    ```
    export S3_ACCESS_KEY_ID=
    export S3_ACCESS_SECRET_KEY=
    export S3_BUCKET=
    ```
- `./add.sh` to begin adding an entry
- `./markdown.sh` to convert all entries into markdown format
    - Format:
        ```
        # YYYYMMDD (End of Week (EoW))
        ### YYYYMMDD - Day (within range of EoW)
        - Entries added to that Day
        ```
    - Preview:
        # YYYYMMDD
        ### YYYYMMDD - Day
        - Entries added to that Day
    - Notes:
        - The markdown output is sorted in descending order by EoW date with the most recent being on top.
        - The Days are sorted in ascending order, Monday to Friday, Friday being on the bottom.
        - The Entries are also sorted in ascending order.
- `./sync.sh` to upload to your S3 bucket
