using System.Collections.Generic;
using System.Threading.Tasks;
using Traffic;

namespace TrafficService
{
    public interface ITrafficBackend
    {
        public Task<List<Camera>> GetCameras();
    }
}