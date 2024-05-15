---
title: Chessli2
emoji: 🏰
colorFrom: blue
colorTo: red
sdk: gradio
app_file: src/chessli2/app.py
pinned: True
---


# Welcome to Chessli2 🏰

[chessli2](https://github.com/pwenker/chessli2) is your **always free** and **open-source** chess trainer 🛡️, designed to elevate your game by allowing you to analyze games, identify mistakes, and sharpen your tactics, all sourced directly from [lichess.org](https://lichess.org/).

## Why a second version?

Incredibly, despite my prolonged absence, I continue to receive heartfelt 💌 thank you notes and eager requests for [chessli](https://github.com/pwenker/chessli). 
This overwhelming support has inspired me to develop a sleek new version of `chessli` that not only squashes all those pesky bugs 🐛 but also introduces a user-friendly graphical interface. This means no programming experience is required to dive in!

## Features 🌟

- **Automatically fetch your games and played tactics puzzles** from lichess via the [berserk python client](https://github.com/lichess-org/berserk) for the Lichess API! 🔄
- **Find your mistakes** by parsing and analyzing your games with [python-chess](https://github.com/niklasf/python-chess) 🔍
- **Leverage the power of spaced repetition** using [Anki](https://apps.ankiweb.net/) with this amazing interactive chess template: [Anki-Chess-2.0](https://github.com/TowelSniffer/Anki-Chess-2.0) 🧠
- And everything with a **beautiful GUI thanks to [gradio](https://www.gradio.app/)**

Chessli2 is here to support your journey to becoming a chess master. Dive in and start enhancing your skills today! 🚀

## Quickstart 🚀

### 👉 Click here to try out the app directly without any setup:
[**Chessli2**](https://pwenker-chessli2.hf.space/)

### 🔍 Inspect code at:
- **GitHub:** [pwenker/chessli2](https://github.com/pwenker/chessli2)
- **Hugging Face Spaces:** [pwenker/chessli2](https://huggingface.co/spaces/pwenker/chessli2)


## Local Deployment 🏠

### Prerequisites 📋

#### Rye 🌾
[Install `Rye`](https://rye-up.com/guide/installation/#installing-rye)
> Rye is a comprehensive tool designed for Python developers. It simplifies your workflow by managing Python installations and dependencies. Simply install Rye, and it takes care of the rest.

### Set-Up 🛠️

Clone the repository, e.g. with:
```
git clone https://github.com/pwenker/chessli2.git
```
Navigate to the directory:
```
cd chessli2
```
And execute:
```
rye sync
```
This creates a virtual environment in `.venv` and synchronizes the repo.

For more details, visit: [Basics - Rye](https://rye-up.com/guide/basics/)

### Start the App 🌟

> [!NOTE]  
> If you choose to install `chessli2` without `rye` just omit `rye run` for the following commands.

Launch the app using:
```
rye run python src/chessli2/app.py
```

Finally, open your browser and visit [http://localhost:7860](http://localhost:7860/) to start practicing!


## Programmatic Access

### API endpoints
Thanks to [Gradio](https://www.gradio.app/), you can find an API documentation for `chessli2` at [Chessli2 API](https://pwenker-chessli2.hf.space/?view=api).

### CLI

There is also a CLI! 
```
rye run chessli2 --help
```

For complete usage information of all commands and options, take a look at the CLI documentation at [docs/cli.md](docs/cli.md).

## FAQ

### 🗝️ How to Obtain Your Lichess API Token

:zap: Fast route: Simply click this pre-filled URL for a quick set-up with the correct token space: https://lichess.org/account/oauth/token/create?scopes[]=puzzle:read&description=My+token+for+chessli2

To acquire a personal API token for the Lichess platform, simply follow these steps:

1. **Create a Lichess Account** 🆕: If you don't already have one, create a Lichess account by visiting [lichess.org](https://lichess.org) and signing up.
2. **Log In** 🔑: After setting up your account, log in and navigate to your account settings.
3. **Access Token Settings** 🔧: Proceed to the 'API Access Tokens' section, typically found under a menu related to tools or personal settings. You can directly access it via [https://lichess.org/account/oauth/token](https://lichess.org/account/oauth/token).
4. **Create a New Token** 🆕: Click on the button to create a new token. You'll need to specify the scopes or permissions that the token should have. These permissions determine what actions your token can perform on your behalf. For `chessli2` it is currently sufficient to permit "Read Puzzle Activity" and "Read Preferences".
5. **Name Your Token** 🏷️: Assign a meaningful name to your token for easy identification, especially useful if managing multiple tokens.
6. **Generate the Token** 🔄: After selecting the necessary scopes and naming your token, click to generate it. Lichess will display your new API token.
7. **Copy and Secure Your Token** 🔒: Ensure you copy and securely store your token. Do not share it, as it grants access to your Lichess account based on the selected scopes. Remember, Lichess will not display the token again once you navigate away from the page.
8. **Use the Token** 🚀: You can now use this token by pasting it into the "Lichess API token" field within the `chessli2` interface

🚨 **Important**: If your token is ever compromised or no longer needed, revoke it immediately to secure your account.

### 📚 How to Get Anki Cards from My Mistakes?

#### 📄 Create a CSV File
- After you've fetched your mistakes with `chessli2`, a "Download CSV" button will appear.  
- Click this button and store the `CSV` file at a location of your choosing.

#### 🛠 Set-up Anki-Chess-2.0
- Next, you will need to set up [Anki-Chess-2.0](https://github.com/TowelSniffer/Anki-Chess-2.0). This is the Anki chess template that is needed to visualize your mistakes within Anki with a beautiful interactive chess board.
- While you are there, why not leave a star ⭐ to show the maintainer that you value the chess template, or send a nice message? 😊 Since the beginnings of `chessli`, the chess template has always been a crucial part!

#### 📥 Import the CSV into Anki

Finally, you can import the CSV file into Anki.

1. Launch the Anki application on your computer.
2. Choose or create the deck into which you want to import the CSV file.
3. Click on the deck name to open it.
4. In the main Anki window, go to the menu bar and click on `File`.
5. Select `Import...` from the dropdown menu.
6. Browse to the location of your CSV file, select it, and click `Open`.
7. Anki will open a dialog box asking how you want to import the CSV file. Select the `Chess-2.0` note type.
8. Make sure it reads: "Field 1 of file is: mapped to PGN" 
9. Click the `Import` button. Anki will process the file and add the new cards to the selected deck.
10. After importing, it’s a good idea to review a few cards to ensure they were imported correctly. You can do this by browsing the deck or starting a study session.
11. Pat yourself on the back! You did it! 🎉
