const mc = require('minecraft-protocol');
const { Client, GatewayIntentBits } = require('discord.js');
require('dotenv').config();

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers
  ]
});

const discordToken = process.env.DISCORD_TOKEN;

const bot = mc.createClient({
  host: process.env.MINECRAFT_HOST,
  port: parseInt(process.env.MINECRAFT_PORT),
  username: 'CalamityItself',
  version: '1.21'
});

bot.on('connect', () => {
  console.log('Connected to the Minecraft server');
});

bot.on('chat', (packet) => {
  const jsonMsg = JSON.parse(packet.message);
  console.log(`Chat: ${jsonMsg}`);
});

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', (message) => {
  if (message.author.bot) return;
  if (message.channel.id === process.env.DISCORD_CHANNEL_ID) {
    bot.write('chat', { message: message.content });
  }
});

client.login(discordToken);
