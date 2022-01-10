# Telegram Bot for SSH Connection

Telegram bot for personal use, providing the ability to connect via Secure Shell (SSH) to the Linux-based machines.

## Installation and Launch

### Using Docker

1. Clone the repository:

```
git clone https://github.com/neuromeow/ssh-telegram-bot
cd ssh-telegram-bot
```

2. Rename environment file from example:

```
mv .env.dist .env
```

3. Personalize configuration by modifying ```.env```:

- Create a new Telegram bot by talking to [@BotFather](https://t.me/BotFather) and get its API token;

- Use some bot like [@my_id_bot](https://t.me/my_id_bot) to get your Telegram user ID;

- Set `BOT_TOKEN` and `BOT_ADMINS` to the values obtained using the steps described above.

4. Install [Docker Compose](https://docs.docker.com/compose/install/).

5. Build and run your container:

```
docker-compose up --build
```

### Manual

1. Clone the repository:

```
git clone https://github.com/neuromeow/ssh-telegram-bot
cd ssh-telegram-bot
```

2. Install Python with [pip](https://pip.pypa.io/en/stable/installing/).

3. Install requirements:

```
pip install -r requirements.txt
```

4. Rename environment file from example:

```
mv .env.dist .env
```

5. Personalize configuration by modifying ```.env```:

- Create a new Telegram bot by talking to [@BotFather](https://t.me/BotFather) and get its API token;

- Use some bot like [@my_id_bot](https://t.me/my_id_bot) to get your Telegram user ID;

- Set `BOT_TOKEN` and `BOT_ADMINS` to the values obtained using the steps described above.

6. Launch bot:

```
python -m bot
```

## Authors

[@neuromeow](https://github.com/neuromeow) for details.

## License

This project is released under the MIT License. See [LICENSE](https://github.com/neuromeow/ssh-telegram-bot/blob/master/LICENSE) for the full licensing condition.
