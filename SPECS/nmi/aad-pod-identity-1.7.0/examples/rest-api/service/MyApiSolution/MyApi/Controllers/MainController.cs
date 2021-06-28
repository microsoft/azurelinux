using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace MyApi.Controllers
{
    [Authorize]
    [Route("")]
    [ApiController]
    public class MainController : ControllerBase
    {
        // GET
        [HttpGet]
        public ActionResult<string> Get()
        {
            return "Hello World";
        }
    }
}