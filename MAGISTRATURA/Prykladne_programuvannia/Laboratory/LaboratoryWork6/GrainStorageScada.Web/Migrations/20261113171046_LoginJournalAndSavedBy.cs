
using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace GrainStorageScada.Web.Migrations
{
    public partial class LoginJournalAndSavedBy : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "LoginEvents",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    UserName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Succeeded = table.Column<bool>(type: "bit", nullable: false),
                    Result = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    IpAddress = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    TimeUtc = table.Column<DateTimeOffset>(type: "datetimeoffset", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_LoginEvents", x => x.Id);
                });

            migrationBuilder.AddColumn<string>(
                name: "SavedBy",
                table: "SensorSamples",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "SavedBy",
                table: "SensorSamples");

            migrationBuilder.DropTable(
                name: "LoginEvents");
        }
    }
}

