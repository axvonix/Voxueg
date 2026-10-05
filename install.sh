set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
pkg update -y
pkg install -y python git curl termux-api traceroute qrencode
chmod +x "$DIR/voxueg.py"
grep -q "alias voxueg=" ~/.bashrc 2>/dev/null || echo "alias voxueg='python $DIR/voxueg.py'" >> ~/.bashrc
echo "Good! Success Next Run: python voxueg.py
