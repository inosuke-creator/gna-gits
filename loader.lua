task.spawn(function()
    local GameId = game.GameId

    print("Detected Game ID:", GameId)

    if GameId == 6701277882 then
        loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/29ca431b9f247ea540933589f1b335d5.lua"))()
    elseif GameId == 6739698191 then
        loadstring(game:HttpGet("https://api.luarmor.net/files/v4/loaders/57c22ad85aad62ca69fbfb0be09b520f.lua"))()
    else
        warn("⚠️ No script found for this Game ID:", GameId)
    end
end)
