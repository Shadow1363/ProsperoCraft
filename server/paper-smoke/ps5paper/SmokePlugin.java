package ps5paper;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
/** Lifecycle, main-thread scheduler and command smoke test; no gameplay changes. */
public final class SmokePlugin extends JavaPlugin {
 public void onEnable(){
  getLogger().info("PS5_PAPER_PLUGIN_ENABLED version=1.0.0");
  getServer().getScheduler().runTaskLater(this,()->getLogger().info("PS5_PAPER_SCHEDULER_OK tick="+getServer().getCurrentTick()),20L);
 }
 public boolean onCommand(CommandSender sender,Command command,String label,String[] args){
  String message="PS5_PAPER_COMMAND_OK tick="+getServer().getCurrentTick()+" players="+getServer().getOnlinePlayers().size();
  getLogger().info(message);sender.sendMessage(message);return true;
 }
 public void onDisable(){getLogger().info("PS5_PAPER_PLUGIN_DISABLED version=1.0.0");}
}
