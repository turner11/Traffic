using Microsoft.AspNetCore.Components;
using Microsoft.JSInterop;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Traffic.Shared
{
    public partial class VideoStreamer
    {
        const string PlayFunctionName = "startPlayer";
        [Inject]
        IJSRuntime JSRuntime { get; set; }
        [Parameter]
        public string Id { get; set; } = "__videoController";
        string _url;
        string Url => this._url ?? "";

        public async Task Start(string url)
        {
            this._url = url;
            await JSRuntime.InvokeVoidAsync(PlayFunctionName, Id);            
        }



    }
}
