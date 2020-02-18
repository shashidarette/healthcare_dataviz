using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(HealthcareDataViz.Startup))]
namespace HealthcareDataViz
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
