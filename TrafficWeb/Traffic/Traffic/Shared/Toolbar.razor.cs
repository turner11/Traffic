using Microsoft.AspNetCore.Components;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Traffic.Shared
{
    public partial class Toolbar
    {
        [CascadingParameter]
        CascadingAppState AppStates { get; set; }
        List<Camera> _cameras;
        List<Camera> Cameras => this._cameras ?? new List<Camera>();
        
        protected override async Task OnParametersSetAsync()
        {
            await base.OnParametersSetAsync();
            this._cameras ??= await this.AppStates?.GetCameras();
        }


        void OnChange(Camera camera)
        {
            this.AppStates.Camera= camera;
        }
    }
}
