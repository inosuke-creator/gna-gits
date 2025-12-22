task.spawn(function()
    local GameId = game.GameId

    print("Detected Game ID:", GameId)

    if GameId == 372226183 then -- FLEE THE FACILITY
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/flee-the-facility.lua"))()
    elseif GameId == 8497165255 then --SPIN A BRAINROT
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/spin-a-brainrot.lua"))()
    elseif GameId == 6701277882 then --FISH IT
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/fish-it.lua"))()
    elseif GameId == 6739698191 then --VIOLENCE DISTRICT
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/vd"))()
    elseif GameId == 7671049560 then --THE FORGE
        loadstring(game:HttpGet("https://raw.githubusercontent.com/inosuke-creator/gna-gits/refs/heads/main/the_forge.lua"))()
    else
        warn("⚠️ No script found for this Game ID:", GameId)
    end
end)
