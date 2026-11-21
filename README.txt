AfinoAi update bundle

Files:
- main.py: refreshed Kivy/OpenRouter chat interface
- requirements.txt: Python dependencies
- assets/icons/: static SVG icon resources
- assets/logo/afinoai_icon.png: app icon artwork

Notes:
- Google sign-in, server-backed account sync, true web search, and secure server-side token accounting are not implemented in this client bundle yet.
- Search toggle currently marks the selected mode in the system instruction; it does not perform a real web search.
- Reasoning depends on whether the selected OpenRouter model supports reasoning.
- Set the Android launcher icon during APK packaging; Pydroid does not automatically change its own app icon.
