local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local player = Players.LocalPlayer

local WEBHOOK_URL = "https://discord.com/api/webhooks/1439957356216717472/OkfHdp2qNDPpTmrfXP2r6HyxVZzE4dqjnM-RGsRIc5JHq3tShK-z5Pys0_A0yU9xFvhT"

local function sendExecutionLog(gameName)
    local username = player.Name
    local displayName = player.DisplayName
    local userId = player.UserId
    local gameId = game.GameId
    local placeName = game.Name
    local timestamp = os.date("%Y-%m-%d %H:%M:%S")

    local data = {
        ["embeds"] = {{
            ["title"] = "Sakura Execution",
            ["description"] = "**Someone just executed the loader!**",
            ["color"] = 16761035,
            ["fields"] = {
                {["name"] = "Username", ["value"] = username .. " (@" .. displayName .. ")", ["inline"] = true},
                {["name"] = "User ID", ["value"] = tostring(userId), ["inline"] = true},
                {["name"] = "Game", ["value"] = placeName .. " (" .. gameName .. ")", ["inline"] = false},
                {["name"] = "Game ID", ["value"] = tostring(gameId), ["inline"] = true},
                {["name"] = "Time", ["value"] = timestamp, ["inline"] = true}
            },
            ["footer"] = {["text"] = "Sakura Logger :two_hearts:"}
        }}
    }

    local requestFunc = syn and syn.request or http_request or request or http.request
    if requestFunc then
        pcall(function()
            requestFunc({
                Url = WEBHOOK_URL,
                Method = "POST",
                Headers = {["Content-Type"] = "application/json"},
                Body = HttpService:JSONEncode(data)
            })
        end)
    end
end

local function onScriptLoad(gameName)
    sendExecutionLog(gameName)
end

task.spawn(function()
    local GameId = game.GameId
    print("Detected Game ID:", GameId)

    if GameId == 372226183 then -- FLEE THE FACILITY
        onScriptLoad("Flee The Facility")
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/flee-the-facility.lua"))()

    elseif GameId == 8497165255 then -- SPIN A BRAINROT
        onScriptLoad("Spin A Brainrot")
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/spin-a-brainrot.lua"))()

    elseif GameId == 6701277882 then -- FISH IT
        onScriptLoad("Fish It")
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/fish-it.lua"))()

    elseif GameId == 6739698191 then -- VIOLENCE DISTRICT
        onScriptLoad("Violence District")
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/vd"))()

    elseif GameId == 7671049560 then -- THE FORGE
        onScriptLoad("The Forge")
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/the_forge.lua"))()

    elseif GameId == 9266873836 then -- ANIME FIGHTING SIMULATOR ENDLESS
        onScriptLoad("Anime Fighting Simulator: Endless")
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/afse.lua"))()

    else
        warn(":warning: No script found for this Game ID:", GameId)
        onScriptLoad("Unknown Game")
    end
end)
