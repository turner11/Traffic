using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using TrafficService;

namespace Traffic
{
    public static class ServiceCollectionExtensions
    {
        public static IServiceCollection AddGrpcService(this IServiceCollection services)
        {
            var address = IPAddress.Parse("127.0.0.1");            
            var ip = new IPEndPoint(address, 50051);
            

            services.AddScoped<ITrafficBackend, TrafficBackend>((s)=> new TrafficBackend(ip));


            return services;
        }
    }
}
