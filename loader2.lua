task.spawn(function()
    local GameId = game.GameId

    print("Detected Game ID:", GameId)

    if GameId == 372226183 then
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/flee-the-facility.lua"))()
    elseif GameId == 8497165255 then
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/spin-a-brainrot.lua"))()
    elseif GameId == 6701277882 then
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/fish-it.lua"))()
    else
        warn("⚠️ No script found for this Game ID:", GameId)
    end
end)
