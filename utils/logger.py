import logging
import discord
from datetime import datetime

class DiscordLogger:
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    async def log_action(self, guild, action_type, user, target=None, reason=None):
        """Log moderator actions to the designated logging channel."""
        log_channel = discord.utils.get(guild.text_channels, name='logs')
        if not log_channel:
            return

        embed = discord.Embed(
            title=f"Moderator Action: {action_type}",
            timestamp=datetime.utcnow(),
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Moderator", value=f"{user.name}#{user.discriminator}")
        
        if target:
            embed.add_field(name="Target", value=f"{target.name}#{target.discriminator}")
        
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)

        try:
            await log_channel.send(embed=embed)
        except discord.Forbidden:
            self.logger.error(f"Cannot send log message in {guild}: Missing permissions")
        except Exception as e:
            self.logger.error(f"Error sending log message: {e}")

    async def log_error(self, guild, error_message):
        """Log errors to the designated logging channel."""
        log_channel = discord.utils.get(guild.text_channels, name='logs')
        if not log_channel:
            return

        embed = discord.Embed(
            title="Error",
            description=error_message,
            timestamp=datetime.utcnow(),
            color=discord.Color.red()
        )

        try:
            await log_channel.send(embed=embed)
        except discord.Forbidden:
            self.logger.error(f"Cannot send error log in {guild}: Missing permissions")
        except Exception as e:
            self.logger.error(f"Error sending error log: {e}")
