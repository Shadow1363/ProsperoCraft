/* SPDX-License-Identifier: Zlib
 * Select up to120Hz from the actual VideoOut inventory, with60Hz fallback.
 * WSI advertises119.88Hz only after OS configuration and vblank verification.
 * Both SDL display reporting and Vulkan surface creation use this policy.
 */
static int PS5_SelectRequestedMode(const VkDisplayModePropertiesKHR *modes,uint32_t count,uint32_t width,uint32_t height)
{
    if(!modes||count==0||count>32||!width||!height)return -1;
    int selected=-1;
    for(uint32_t i=0;i<count;i++){
        VkDisplayModeParametersKHR p=modes[i].parameters;
        if(p.visibleRegion.width!=width||p.visibleRegion.height!=height||p.refreshRate==0||p.refreshRate>120000)continue;
        if(selected<0||p.refreshRate>modes[selected].parameters.refreshRate)selected=(int)i;
    }
    return selected;
}

static int PS5_SelectDisplayMode(const VkDisplayModePropertiesKHR *modes,uint32_t count,VkExtent2D native)
{
    (void)native;
    return PS5_SelectRequestedMode(modes,count,1920,1080);
}
