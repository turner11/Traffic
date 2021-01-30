using Microsoft.AspNetCore.Components;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using TrafficService;

namespace Traffic.Shared
{
    public partial class CascadingAppState
    {
        [Inject]
        ITrafficBackend trafficBackend { get; set; }
        [Parameter]
        public RenderFragment ChildContent { get; set; }

        Camera _camera;
        public Camera Camera
        {
            get => this._camera; 
            internal set
            {
                this._camera = value;
                this.StateHasChanged();
            }
        }

        internal async Task<List<Camera>> GetCameras()
        {
            return await this.trafficBackend.GetCameras();
        }
    }
}
