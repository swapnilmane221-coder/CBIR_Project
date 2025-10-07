import pickle, os

# Old path prefix (from Google Colab)
OLD_PREFIX = "/content/drive/MyDrive/Ds lab/images"

# New path prefix on your local system
NEW_PREFIX = os.path.join(os.getcwd(), "CBIR_PROJECT", "media", "images")

# Full path to your existing paths.pkl
PKL_PATH = os.path.join(os.getcwd(), "models", "paths.pkl")

print(f"🔧 Updating paths.pkl at: {PKL_PATH}")
print(f"Replacing:\n  {OLD_PREFIX}\n➡ {NEW_PREFIX}\n")

# Load existing paths
with open(PKL_PATH, "rb") as f:
    paths = pickle.load(f)

# Replace old prefix with new one
new_paths = [p.replace(OLD_PREFIX, NEW_PREFIX) for p in paths]

# Save updated paths.pkl
with open(PKL_PATH, "wb") as f:
    pickle.dump(new_paths, f)

# Verify one example
print("✅ Updated paths.pkl successfully!")
print("Example old path:")
print("  ", paths[0])
print("Example new path:")
print("  ", new_paths[0])
