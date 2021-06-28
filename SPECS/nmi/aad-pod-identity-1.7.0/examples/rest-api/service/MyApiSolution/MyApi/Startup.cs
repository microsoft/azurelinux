using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace MyApi
{
    public class Startup
    {
        private static readonly string _tenantId;
        private static readonly string _applicationId;

        static Startup()
        {
            _tenantId = Environment.GetEnvironmentVariable("TENANT_ID");
            _applicationId = Environment.GetEnvironmentVariable("APPLICATION_ID");

            if (string.IsNullOrWhiteSpace(_tenantId))
            {
                throw new ArgumentNullException("Environment variable TENANT_ID needs to be defined");
            }
            if (string.IsNullOrWhiteSpace(_applicationId))
            {
                throw new ArgumentNullException("Environment variable APPLICATION_ID needs to be defined");
            }
        }

        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services
                .AddAuthentication()
                .AddJwtBearer(options =>
                {
                    options.Audience = _applicationId;
                    options.Authority = $"https://sts.windows.net/{_tenantId}/";
                });
            services.AddAuthorization(options =>
            {
                var defaultAuthorizationPolicyBuilder = new AuthorizationPolicyBuilder(
                    JwtBearerDefaults.AuthenticationScheme);

                defaultAuthorizationPolicyBuilder =
                    defaultAuthorizationPolicyBuilder.RequireAuthenticatedUser();
                options.DefaultPolicy = defaultAuthorizationPolicyBuilder.Build();
            });
            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_1);
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseMvc();
        }
    }
}
