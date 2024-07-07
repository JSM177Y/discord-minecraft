require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const mineflayer = require('mineflayer');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
const discordToken = process.env.DISCORD_TOKEN;
const minecraftOptions = {
  host: 'your.minecraft.server.ip',
  port: 25565,
  username: 'yourMinecraftUsername',
  password: 'yourMinecraftPassword'
};

const bot = mineflayer.createBot(minecraftOptions);

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

bot.on('login', () => {
  console.log(`Minecraft bot logged in as ${bot.username}`);
});

bot.on('chat', (username, message) => {
  if (username === bot.username) return;
  const channel = client.channels.cache.get('YOUR_DISCORD_CHANNEL_ID');
  if (channel) {
    channel.send(`**${username}**: ${message}`);
  }
});

client.on('messageCreate', message => {
  if (message.author.bot) return;
  if (message.channel.id === 'YOUR_DISCORD_CHANNEL_ID') {
    bot.chat(message.content);
  }
});

client.login(discordToken);