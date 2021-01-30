using Microsoft.AspNetCore.Components;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Traffic.Shared;

namespace Traffic.Pages
{
    public partial class Index
    {
        [CascadingParameter]
        CascadingAppState AppState { get; set; }
    }
}
