using Grpc.Core;
using Grpc.Net.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using TrafficService;

namespace Traffic
{
    public class TrafficBackend : ITrafficBackend
    {
        Channel Channel { get; }
        public TrafficBackend(IPEndPoint endpoint)
        {
            
            if (endpoint is null)
                throw new ArgumentNullException(nameof(endpoint));

            
            //IReadOnlyList<ChannelOption> options = new List<ChannelOption> {
            //  new ChannelOption(ChannelOptions.MaxReceiveMessageLength, maxMessageSizeMB * 1024 * 1024),
            //  new ChannelOption("grpc.keepalive_permit_without_calls", 1)}.AsReadOnly();

            var channel = new Channel(endpoint.ToString(), ChannelCredentials.Insecure);


            this.Channel = channel;
            //String user = "you";
        }


        public async Task<List<Camera>> GetCameras()
        {
            var client = new TrafficService.TrafficServiceClient(this.Channel);
            CamerasReply reply = await client.GetCamerasAsync(new CamerasRequest()).ResponseAsync;
            return reply.Cameras.ToList();
        }
    }
}
