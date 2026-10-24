using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.Domain.Entities;

namespace WEB_453503_Khalamau.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GemTypesController : ControllerBase
    {
        private readonly AppDbContext _context;

        public GemTypesController(AppDbContext context)
        {
            _context = context;
        }

        // GET: api/GemTypes
        [HttpGet]
        public async Task<ActionResult<IEnumerable<GemType>>> GetGemTypes()
        {
            return await _context.GemTypes.ToListAsync();
        }

        // GET: api/GemTypes/5
        [HttpGet("{id}")]
        public async Task<ActionResult<GemType>> GetGemType(int id)
        {
            var gemType = await _context.GemTypes.FindAsync(id);

            if (gemType == null)
            {
                return NotFound();
            }

            return gemType;
        }

        // PUT: api/GemTypes/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutGemType(int id, GemType gemType)
        {
            if (id != gemType.Id)
            {
                return BadRequest();
            }

            _context.Entry(gemType).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!GemTypeExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/GemTypes
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<GemType>> PostGemType(GemType gemType)
        {
            _context.GemTypes.Add(gemType);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetGemType", new { id = gemType.Id }, gemType);
        }

        // DELETE: api/GemTypes/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteGemType(int id)
        {
            var gemType = await _context.GemTypes.FindAsync(id);
            if (gemType == null)
            {
                return NotFound();
            }

            _context.GemTypes.Remove(gemType);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool GemTypeExists(int id)
        {
            return _context.GemTypes.Any(e => e.Id == id);
        }
    }
}
