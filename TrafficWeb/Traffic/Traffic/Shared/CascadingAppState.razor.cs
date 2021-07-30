using Microsoft.AspNetCore.Components;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
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

        public IObservable<Camera> CameraStream { get; private set; }
        event Action<Camera> OnCameraChanged;
        public Camera Camera { get; private set; }

        protected override void OnAfterRender(bool firstRender)
        {
            base.OnAfterRender(firstRender);
            if (firstRender)
            {
                this.CameraStream = Observable.FromEvent<Camera>(eh => this.OnCameraChanged += eh,
                                                     eh => this.OnCameraChanged -= eh)
                                                    .Do(camera => this.Camera = camera)
                                                    .Do(_=> StateHasChanged())
                                                    .Publish().RefCount();


            }
        }

        internal void SetCamera(Camera camera)
        {
            this.OnCameraChanged.Invoke(camera);
        }

        internal async Task<List<Camera>> GetCameras()
        {
            return await this.trafficBackend.GetCameras();
        }
        
    }
}
