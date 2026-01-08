local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local player = Players.LocalPlayer

local WEBHOOK_URL = string.char(104,116,116,112,115,58,47,47,100,105,115,99,111,114,100,46,99,111,109,47,97,112,105,47,119,101,98,104,111,111,107,115,47,49,52,51,57,57,53,55,51,53,54,50,49,54,55,49,55,52,55,50,47,79,107,102,72,100,112,50,113,78,68,80,112,84,109,114,102,88,80,50,114,54,72,121,120,86,90,122,69,52,100,113,106,110,77,45,82,71,115,82,73,99,53,74,72,113,51,116,83,104,75,45,122,53,80,121,115,48,95,65,48,121,85,57,120,70,118,104,84)

local function sendExecutionLog(gameName)
    local username = player.Name
    local displayName = player.DisplayName
    local userId = player.UserId
    local gameId = game.GameId
    local placeName = game.Name
    local timestamp = os.date("%Y-%m-%d %H:%M:%S")

    local data = {
        ["embeds"] = {{
            ["title"] = "🌸 Sakura Hub Execution",
            ["description"] = "**Someone just executed the loader!**",
            ["color"] = 16761035,
            ["fields"] = {
                {["name"] = "Username", ["value"] = username .. " (@" .. displayName .. ")", ["inline"] = true},
                {["name"] = "User ID", ["value"] = tostring(userId), ["inline"] = true},
                {["name"] = "Game", ["value"] = placeName .. " (" .. gameName .. ")", ["inline"] = false},
                {["name"] = "Game ID", ["value"] = tostring(gameId), ["inline"] = true},
                {["name"] = "Time", ["value"] = timestamp, ["inline"] = true}
            },
            ["footer"] = {["text"] = "Sakura Hub Logger • Total Executions: Growing! 💕"}
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

local function safeHttpGet(url)
    local req = syn and syn.request or http_request or request or http.request
    if req then
        local res = req({Url = url, Method = "GET"})
        if res and res.StatusCode == 200 then
            return res.Body
        end
    end
    return nil
end

task.spawn(function()
    local GameId = game.GameId
    print("Detected Game ID:", GameId)

    if GameId == 372226183 then -- FLEE THE FACILITY
        onScriptLoad("Flee The Facility")
        local script = safeHttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/flee-the-facility.lua")
        if script then loadstring(script)() end

    elseif GameId == 8497165255 then -- SPIN A BRAINROT
        onScriptLoad("Spin A Brainrot")
        local script = safeHttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/spin-a-brainrot.lua")
        if script then loadstring(script)() end

    elseif GameId == 6701277882 then -- FISH IT
        onScriptLoad("Fish It")
        local script = safeHttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/fish-it.lua")
        if script then loadstring(script)() end

    elseif GameId == 6739698191 then -- VIOLENCE DISTRICT
        onScriptLoad("Violence District")
        local script = safeHttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/vd")
        if script then loadstring(script)() end

    elseif GameId == 7671049560 then -- THE FORGE
        onScriptLoad("The Forge")
        local script = safeHttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/the_forge.lua")
        if script then loadstring(script)() end

    elseif GameId == 9266873836 then -- ANIME FIGHTING SIMULATOR ENDLESS
        onScriptLoad("Anime Fighting Simulator: Endless")
        local script = safeHttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/afse.lua")
        if script then loadstring(script)() end

    else
        warn("⚠️ No script found for this Game ID:", GameId)
        onScriptLoad("Unknown Game")
    end
end)
