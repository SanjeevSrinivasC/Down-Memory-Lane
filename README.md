# Down Memory Lane 🕰️📸

A Slack bot that generates nostalgic "childhood photos" using AI. Simply mention the bot in Slack with a description, and it creates realistic old family photographs using a personalized Flux LoRA model trained on your face.

## Features

- **Natural Language Processing**: Extracts age information from casual requests like "my 5-year-old self"
- **Personalized AI Generation**: Uses your custom Flux LoRA model hosted on Replicate
- **Slack Integration**: Works seamlessly within Slack channels and threads
- **Automatic Prompt Enhancement**: Converts simple requests into detailed prompts for better results
- **Thread-Safe**: Responds in threads to keep channels organized

## How It Works

1. Mention the bot in Slack: `@Down Memory Lane my 5-year-old self on a beach`
2. The bot extracts the age and scene from your request
3. It builds a detailed prompt for the AI model
4. Generates a nostalgic childhood photo using your trained LoRA model
5. Uploads the image directly to the Slack thread

## Setup Instructions

### 1. Prerequisites

- Python 3.7+
- A Slack workspace with bot permissions
- A Replicate account with a trained Flux LoRA model
- Git (for cloning the repository)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/SanjeevSrinivasC/Down-Memory-Lane.git
cd Down-Memory-Lane

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Slack App Configuration

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app
2. Enable Socket Mode and generate an App-Level Token
3. Add the following Bot Token Scopes:
   - `app_mentions:read`
   - `channels:history`
   - `chat:write`
   - `files:write`
4. Install the app to your workspace and copy the Bot User OAuth Token

### 4. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
```

Fill in your `.env` file with:

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-level-token
REPLICATE_API_TOKEN=r8_your-replicate-token
REPLICATE_MODEL=your-username/your-model-name:version-id
TRIGGER_WORD=TOK
LORA_SCALE=0.9
```

### 5. Running the Bot

```bash
python app.py
```

You should see: `Down Memory Lane bot is running... (press Ctrl+C to stop)`

## Usage Examples

In any Slack channel where the bot is present:

- `@Down Memory Lane my 5-year-old self playing in the park`
- `@Down Memory Lane 3-year-old me at a birthday party`
- `@Down Memory Lane my 7-year-old self riding a bicycle`
- `@Down Memory Lane 6 year old me on Christmas morning`

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SLACK_BOT_TOKEN` | Your Slack bot token (required) | - |
| `SLACK_APP_TOKEN` | Your Slack app-level token (required) | - |
| `REPLICATE_API_TOKEN` | Your Replicate API token (required) | - |
| `REPLICATE_MODEL` | Your trained Flux LoRA model ID (required) | - |
| `TRIGGER_WORD` | The trigger word for your LoRA model | `TOK` |
| `LORA_SCALE` | Strength of the LoRA effect (0.0-1.0) | `0.9` |

### Customization

- **Age Detection**: Automatically detects ages like "5-year-old", "3 year old", etc.
- **Scene Processing**: Extracts scene descriptions while removing age phrases
- **Prompt Enhancement**: Adds professional photography descriptors for better results

## Technical Details

### Dependencies

- **slack_bolt**: Modern Slack SDK for Python
- **replicate**: Client for Replicate AI platform
- **requests**: HTTP library for downloading generated images
- **python-dotenv**: Environment variable management

### Architecture

```
User Request → Age/Scene Extraction → Prompt Building → AI Generation → Image Upload
```

### Error Handling

- Graceful handling of API failures
- User-friendly error messages in Slack
- Comprehensive logging for debugging

## Troubleshooting

### Common Issues

1. **Bot doesn't respond**: Check that the bot is invited to the channel and tokens are correct
2. **Image generation fails**: Verify your Replicate model ID and API token
3. **Slow responses**: Image generation typically takes 20-60 seconds

### Logs

The bot logs all activities to the console. Check the output for detailed error messages.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source. Feel free to modify and distribute as needed.

## Acknowledgments

- Built with [Slack Bolt for Python](https://slack.dev/bolt-python/)
- AI generation powered by [Replicate](https://replicate.com/)
- Uses Flux LoRA models for personalized image generation

---

**Note**: This bot requires a pre-trained Flux LoRA model with your face data. The model should be hosted on Replicate and accessible via API.
