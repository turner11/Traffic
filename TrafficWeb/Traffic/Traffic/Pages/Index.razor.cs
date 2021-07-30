using Microsoft.AspNetCore.Components;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using System.Threading.Tasks;
using Traffic.Shared;

namespace Traffic.Pages
{
    public partial class Index: IDisposable
    {
        private IDisposable cameraSubscription;

        [CascadingParameter]
        CascadingAppState AppState { get; set; }


        VideoStreamer RawVideoStreamer { get; set; }
        public bool ShowCameraElements { get; private set; }

        protected override void OnAfterRender(bool firstRender)
        {
            base.OnAfterRender(firstRender);
            if (firstRender)
            {
                this.cameraSubscription = 
                    this.AppState.CameraStream.Do(Camera =>
                    {
                        var showCameraElements = Camera != null;
                        var stateChanged = showCameraElements != this.ShowCameraElements;
                        this.ShowCameraElements = showCameraElements;
                        if (stateChanged)
                            this.StateHasChanged();
                    })
                    .Subscribe(async camera => await HandleCameraChanged(camera));
                
            }
        }

        private async Task HandleCameraChanged(Camera camera)
        {
            if (this.ShowCameraElements && camera != null)
            {
             //   await this.RawVideoStreamer.Start(camera.Url);
            }
        }

        public void Dispose()
        {
            this.cameraSubscription?.Dispose();
            this.cameraSubscription = null;
        }
    }
}
