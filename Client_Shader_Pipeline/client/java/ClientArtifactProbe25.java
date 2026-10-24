import java.io.InputStream;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.Properties;

/** Hash and class-loading preflight only: never invokes the game or graphics. */
public final class ClientArtifactProbe25 {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Prepared build/client directory required");
        Path root = Path.of(args[0]);
        Properties inventory = new Properties();
        try (InputStream input = Files.newInputStream(root.resolve("client-inventory.properties"))) {
            inventory.load(input);
        }
        if (inventory.size() != 54) throw new IllegalStateException("Expected 54 pinned client/Java JARs");
        ArrayList<URL> urls = new ArrayList<>();
        for (String file : inventory.stringPropertyNames().stream().sorted().toList()) {
            Path jar = root.resolve("jars").resolve(file);
            String hash = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(jar)));
            if (!hash.equals(inventory.getProperty(file))) throw new IllegalStateException("Hash mismatch: " + file);
            urls.add(jar.toUri().toURL());
        }
        try (URLClassLoader loader = new URLClassLoader(urls.toArray(URL[]::new), ClassLoader.getPlatformClassLoader())) {
            for (String name : new String[] {
                "net.minecraft.client.main.Main",
                "com.mojang.blaze3d.platform.Window",
                "com.mojang.blaze3d.platform.SDLEventHandler",
                "com.mojang.renderpearl.backend.vulkan.VulkanBackend",
                "com.mojang.renderpearl.backend.vulkan.VulkanInstance",
                "org.lwjgl.sdl.SDLVulkan",
                "org.lwjgl.vulkan.VK12"
            }) {
                Class.forName(name, false, loader);
                System.out.println("MC_CLIENT_CLASS_OK " + name + " initialized=false");
            }
            System.out.println("MC_CLIENT_ARTIFACT_PREFLIGHT_OK jars=54; no native initialization, GPU, login or game launch attempted");
        }
    }
}
