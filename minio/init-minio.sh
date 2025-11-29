#!/bin/sh

# Set the MinIO server command
MINIO_COMMAND="/usr/bin/minio server /data --console-address :9001"

# Define the buckets you want to create (space-separated list)
BUCKETS="staging raw curated logging backup"

# Define the specific folder/prefix for Spark logs
LOGGING_BUCKET="logging"
SPARK_EVENTS_FOLDER="spark-events"

# 1. Start MinIO in the background
$MINIO_COMMAND &

# 2. Wait for MinIO to become available (required for 'mc' to connect)
/usr/bin/mc wait --timeout 30 http://localhost:9000

# 3. Configure the 'local' alias for the 'mc' client
# 'mc' needs to know how to connect to the running server.
/usr/bin/mc alias set local http://localhost:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

# 4. Create the required primary buckets
for bucket in $BUCKETS; do
    echo "Creating bucket: $bucket"
    # Use 'mb' (make bucket) with the --ignore-existing flag to prevent errors on restart
    /usr/bin/mc mb local/$bucket --ignore-existing
done

# --- NEW STEP: Create the Spark Events folder/prefix ---
echo "Creating Spark Events folder inside the logging bucket..."

# Create a temporary dummy file
TEMP_FILE=$(mktemp)

# Create an object with a key that includes the folder name and a trailing slash.
# This explicitly creates the S3 "folder" structure.
# NOTE: The destination path is local/bucket_name/folder_name/ (trailing slash ensures it's a folder)
/usr/bin/mc cp "$TEMP_FILE" "local/${LOGGING_BUCKET}/${SPARK_EVENTS_FOLDER}/.placeholder"

# Remove the temporary file
rm "$TEMP_FILE"

echo "Folder ${LOGGING_BUCKET}/${SPARK_EVENTS_FOLDER}/ created."
echo "MinIO initialization complete. Buckets and Spark Events folder created."

# 5. Bring the background MinIO process back to the foreground
# This keeps the container running indefinitely.
wait