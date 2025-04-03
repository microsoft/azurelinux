set -eux
echo "Kangaroo" | tee --append /log.txt
echo "Working dir: $(pwd)" | tee --append /log.txt

# Ensure files in the config's directory as accessible to scripts.
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cp "$SCRIPT_DIR/../files/a.txt" /
