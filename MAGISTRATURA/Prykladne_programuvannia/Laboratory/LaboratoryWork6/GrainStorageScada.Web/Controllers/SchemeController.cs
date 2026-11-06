
using GrainStorageScada.Web.Data;
using GrainStorageScada.Web.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace GrainStorageScada.Web.Controllers
{
    [Authorize]
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
        [Authorize(Policy = "CanReadSavings")]
        public async Task<IActionResult> Save()
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

            await _db.SaveChangesAsync();

            return RedirectToAction("History");
        }

        public async Task<IActionResult> History()
        {
            var samples = await _db.SensorSamples
                .OrderByDescending(s => s.Id)
                .Take(50)
                .ToListAsync();

            return View(samples);
        }
    }
}

