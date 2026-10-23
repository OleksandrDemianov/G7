using GrainStorageScada.Web.Data;
using GrainStorageScada.Web.Services;
using Microsoft.AspNetCore.Mvc;

namespace GrainStorageScada.Web.Controllers
{
    public class SchemeController : Controller
    {
        private readonly LiveValuesCache _cache;
        private readonly ApplicationDbContext _db;

        public SchemeController(
            LiveValuesCache cache,
            ApplicationDbContext db)
        {
            _cache = cache;
            _db = db;
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

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Save()
        {
            foreach (var r in _cache.GetAll())
            {
                _db.SensorSamples.Add(new SensorSample
                {
                    Topic = r.Topic,
                    Value = r.Value,
                    Unit = r.Unit,
                    MeasuredAtUtc = r.MeasuredAtUtc
                });
            }

            _db.SaveChanges();

            return RedirectToAction("History");
        }

        public IActionResult History()
        {
            var samples = _db.SensorSamples
                .OrderByDescending(s => s.Id)
                .Take(50)
                .ToList();

            return View(samples);
        }
    }
}
