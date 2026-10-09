
using GrainStorageScada.Web.Services;
using Microsoft.AspNetCore.Mvc;

namespace GrainStorageScada.Web.Controllers
{
    public class SchemeController : Controller
    {
        private readonly LiveValuesCache _cache;

        public SchemeController(LiveValuesCache cache)
        {
            _cache = cache;
        }

        public IActionResult Index()
        {
            return View();
        }

        [HttpGet]
        public IActionResult Readings()
        {
            return Json(_cache.GetAll());
        }
    }
}

