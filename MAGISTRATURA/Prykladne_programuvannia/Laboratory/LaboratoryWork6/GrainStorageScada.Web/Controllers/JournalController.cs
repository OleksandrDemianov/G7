using GrainStorageScada.Web.Data;
using GrainStorageScada.Web.Security;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace GrainStorageScada.Web.Controllers
{
    [Authorize(Roles = AppRoles.Admin)]
    public class JournalController : Controller
    {
        private readonly ApplicationDbContext _db;

        public JournalController(ApplicationDbContext db)
        {
            _db = db;
        }

        public async Task<IActionResult> Index()
        {
            var events = await _db.LoginEvents
                .OrderByDescending(e => e.Id)
                .Take(100)
                .ToListAsync();

            return View(events);
        }
    }
}
