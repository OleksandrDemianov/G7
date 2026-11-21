using GrainStorageScada.Web.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace GrainStorageScada.Web.Controllers;

[Authorize(Policy = "CanConfigure")]
public class SettingsController : Controller
{
    private readonly SchemeConfigService _scheme;

    public SettingsController(SchemeConfigService scheme)
    {
        _scheme = scheme;
    }

    public IActionResult Index()
    {
        return View(_scheme.GetThresholds());
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult UpdateMax(string topic, int max)
    {
        if (max < -50 || max > 150)
        {
            TempData["Message"] =
                "Threshold must be between -50 and 150.";

            return RedirectToAction("Index");
        }

        if (!_scheme.UpdateMax(topic, max))
        {
            return NotFound();
        }

        TempData["Message"] =
            "Threshold saved by " + User.Identity?.Name;

        return RedirectToAction("Index");
    }
}
