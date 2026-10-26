/* SPDX-License-Identifier: Zlib
 * Choose an actual enumerated mode;prefer1080p at normal refresh for startup.
 * Both SDL's display inventory and Vulkan surface creation use this policy.
 */
static int PS5_SelectDisplayMode(const VkDisplayModePropertiesKHR *modes,uint32_t count,VkExtent2D native)
{
    if(!modes||count==0||count>32)return -1;
    int selected=-1,best=-1;
    for(uint32_t i=0;i<count;i++){
        VkDisplayModeParametersKHR p=modes[i].parameters;
        if(p.visibleRegion.width<640||p.visibleRegion.width>3840||p.visibleRegion.height<480||p.visibleRegion.height>2160||p.refreshRate==0)continue;
        int score=(p.refreshRate<=60000?4:0)+(p.visibleRegion.width==1920&&p.visibleRegion.height==1080?2:0)+(p.visibleRegion.width==native.width&&p.visibleRegion.height==native.height?1:0);
        if(score>best||(score==best&&p.refreshRate>modes[selected].parameters.refreshRate)){selected=(int)i;best=score;}
    }
    return selected;
}
