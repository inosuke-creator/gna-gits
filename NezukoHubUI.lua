local NezukoHub = {}
NezukoHub.__index = NezukoHub

local UIS = game:GetService("UserInputService")

-- Create main window
function NezukoHub:CreateWindow(config)
    local Window = {}

    -- ScreenGui
    local gui = Instance.new("ScreenGui")
    gui.Name = config.Name or "NezukoHub"
    gui.Parent = game.CoreGui

    -- Main frame
    local main = Instance.new("Frame")
    main.Name = "Main"
    main.Parent = gui
    main.Size = UDim2.new(0, 500, 0, 320)
    main.Position = UDim2.new(0.5, -250, 0.5, -160)
    main.BackgroundColor3 = Color3.fromRGB(25,25,25)
    main.Active = true
    main.Draggable = true

    -- Title bar
    local titleBar = Instance.new("Frame")
    titleBar.Parent = main
    titleBar.Size = UDim2.new(1, 0, 0, 40)
    titleBar.BackgroundColor3 = Color3.fromRGB(32,32,32)

    -- Title text
    local title = Instance.new("TextLabel")
    title.Parent = titleBar
    title.Size = UDim2.new(1, -80, 1, 0)
    title.Position = UDim2.new(0, 0, 0, 0)
    title.Text = config.Name or "Nezuko Hub"
    title.TextColor3 = Color3.new(1,1,1)
    title.Font = Enum.Font.GothamBold
    title.TextSize = 20
    title.BackgroundTransparency = 1

    -- Minimize button
    local minimize = Instance.new("TextButton")
    minimize.Parent = titleBar
    minimize.Size = UDim2.new(0, 40, 1, 0)
    minimize.Position = UDim2.new(1, -80, 0, 0)
    minimize.Text = "_"
    minimize.Font = Enum.Font.GothamBold
    minimize.TextSize = 20
    minimize.TextColor3 = Color3.new(1,1,1)
    minimize.BackgroundColor3 = Color3.fromRGB(50,50,50)

    local minimized = false
    minimize.MouseButton1Click:Connect(function()
        minimized = not minimized
        for _, v in pairs(main:GetChildren()) do
            if v ~= titleBar then
                v.Visible = not minimized
            end
        end
        main.Size = minimized and UDim2.new(0,500,0,40) or UDim2.new(0,500,0,320)
    end)

    -- Close button
    local closeBtn = Instance.new("TextButton")
    closeBtn.Parent = titleBar
    closeBtn.Size = UDim2.new(0, 40, 1, 0)
    closeBtn.Position = UDim2.new(1, -40, 0, 0)
    closeBtn.Text = "X"
    closeBtn.Font = Enum.Font.GothamBold
    closeBtn.TextSize = 20
    closeBtn.TextColor3 = Color3.new(1,1,1)
    closeBtn.BackgroundColor3 = Color3.fromRGB(200,50,50)

    closeBtn.MouseButton1Click:Connect(function()
        gui:Destroy()
    end)

    Window.GUI = gui
    Window.Main = main

    setmetatable(Window, {__index = NezukoHub})
    return Window
end

-- Create a tab with scrollable page
function NezukoHub:CreateTab(config)
    local Tab = {}

    -- Tab button
    local button = Instance.new("TextButton")
    button.Parent = self.Main
    button.Size = UDim2.new(0, 120, 0, 28)
    button.Position = UDim2.new(0, 10, 0, 50 + (#self.Main:GetChildren()*30))
    button.Text = config.Name
    button.BackgroundColor3 = Color3.fromRGB(40,40,40)
    button.Font = Enum.Font.Gotham
    button.TextColor3 = Color3.new(1,1,1)
    button.TextSize = 14
    button.AutoButtonColor = true

    -- Scrolling frame for the tab page
    local page = Instance.new("ScrollingFrame")
    page.Name = "Page"
    page.Parent = self.Main
    page.Size = UDim2.new(1, -140, 1, -60)
    page.Position = UDim2.new(0, 135, 0, 50)
    page.BackgroundColor3 = Color3.fromRGB(30,30,30)
    page.Visible = false
    page.CanvasSize = UDim2.new(0,0,0,0)
    page.ScrollBarThickness = 6
    page.AutomaticCanvasSize = Enum.AutomaticSize.Y
    page.VerticalScrollBarInset = Enum.ScrollBarInset.ScrollBar

    -- Show/hide page when tab clicked
    button.MouseButton1Click:Connect(function()
        for _, v in pairs(self.Main:GetChildren()) do
            if v:IsA("ScrollingFrame") and v.Name == "Page" then
                v.Visible = false
            end
        end
        page.Visible = true
    end)

    Tab.Page = page
    Tab.TogglesCount = 0 -- track toggles for proper stacking

    setmetatable(Tab, {__index = NezukoHub})
    return Tab
end

-- Create toggle inside a tab
function NezukoHub:CreateToggle(config)
    local Tab = config.Tab
    if not Tab then return end
    Tab.TogglesCount = (Tab.TogglesCount or 0) + 1

    local btn = Instance.new("TextButton")
    btn.Parent = Tab.Page
    btn.Size = UDim2.new(1, -20, 0, 32)
    btn.Position = UDim2.new(0, 10, 0, 10 + (Tab.TogglesCount - 1) * 40)
    btn.Text = config.Name or "Toggle"
    btn.Font = Enum.Font.Gotham
    btn.TextSize = 14
    btn.TextColor3 = Color3.new(1,1,1)
    btn.BackgroundColor3 = Color3.fromRGB(45,45,45)

    local state = false
    btn.MouseButton1Click:Connect(function()
        state = not state
        btn.BackgroundColor3 = state and Color3.fromRGB(0,170,0) or Color3.fromRGB(45,45,45)
        if config.Callback then
            pcall(config.Callback, state)
        end
    end)

    return btn
end

-- Create a teleport list inside a tab (1 per row, scrollable, styled like home tab)
function NezukoHub:CreateTeleportList(config)
    local Tab = config.Tab
    local destinations = config.Destinations
    if not Tab or not destinations then return end

    Tab.TogglesCount = Tab.TogglesCount or 0
    local yOffset = 10 + (Tab.TogglesCount * 40)

    -- Scrolling frame inside the tab page
    local ScrollFrame = Instance.new("ScrollingFrame")
    ScrollFrame.Parent = Tab.Page
    ScrollFrame.Size = UDim2.new(1, -20, 1, -yOffset - 10)
    ScrollFrame.Position = UDim2.new(0, 10, 0, yOffset)
    ScrollFrame.BackgroundColor3 = Color3.fromRGB(50,50,50)
    ScrollFrame.ScrollBarThickness = 6
    ScrollFrame.CanvasSize = UDim2.new(0,0,0,0)
    ScrollFrame.AutomaticCanvasSize = Enum.AutomaticSize.Y

    local internalYOffset = 10

    -- Info label
    local Label = Instance.new("TextLabel")
    Label.Text = "Click a destination to teleport instantly:"
    Label.Size = UDim2.new(1, -20, 0, 20)
    Label.Position = UDim2.new(0, 10, 0, internalYOffset)
    Label.TextColor3 = Color3.new(1,1,1)
    Label.Font = Enum.Font.Gotham
    Label.TextSize = 14
    Label.BackgroundTransparency = 1
    Label.TextXAlignment = Enum.TextXAlignment.Left
    Label.Parent = ScrollFrame
    internalYOffset += 30

    local buttonHeight = 32
    local padding = 10
    local maxY = internalYOffset

    for i, data in ipairs(destinations) do
        local name, position = data[1], data[2]

        local TeleButton = Instance.new("TextButton")
        TeleButton.Size = UDim2.new(1, -20, 0, buttonHeight)
        TeleButton.Position = UDim2.new(0, 10, 0, internalYOffset)
        TeleButton.BackgroundColor3 = Color3.fromRGB(45,45,45)
        TeleButton.TextColor3 = Color3.new(1,1,1)
        TeleButton.Font = Enum.Font.Gotham
        TeleButton.TextSize = 14
        TeleButton.Text = name
        TeleButton.Parent = ScrollFrame

        TeleButton.MouseButton1Click:Connect(function()
            if config.Callback then
                pcall(config.Callback, name, position)
            end
        end)

        internalYOffset += buttonHeight + padding
        maxY = internalYOffset
    end

    ScrollFrame.CanvasSize = UDim2.new(0, 0, 0, maxY)
end

-- First, create the window
local Window = NezukoHub:CreateWindow({Name = "Nezuko Hub"})

-- Create other tabs
local HomeTab = Window:CreateTab({Name = "Home"})
local TeleportTab = Window:CreateTab({Name = "Teleport"})
local AboutTab = Window:CreateTab({Name = "About"})  -- Make sure this exists before adding content

-- Now you can safely add content to the About tab
-- Add text label
local infoLabel = Instance.new("TextLabel")
infoLabel.Parent = AboutTab.Page
infoLabel.Size = UDim2.new(1, -20, 0, 60)
infoLabel.Position = UDim2.new(0, 10, 0, 10)
infoLabel.Text = "For future updates or sneak peeks, kindly join this Discord server:"
infoLabel.TextColor3 = Color3.new(1,1,1)
infoLabel.Font = Enum.Font.Gotham
infoLabel.TextSize = 14
infoLabel.TextWrapped = true
infoLabel.BackgroundTransparency = 1
infoLabel.TextXAlignment = Enum.TextXAlignment.Left

-- Add "Join Discord Server" button
local discordButton = Instance.new("TextButton")
discordButton.Parent = AboutTab.Page
discordButton.Size = UDim2.new(0, 200, 0, 35)
discordButton.Position = UDim2.new(0, 10, 0, 80)
discordButton.BackgroundColor3 = Color3.fromRGB(45,45,45)
discordButton.TextColor3 = Color3.new(1,1,1)
discordButton.Font = Enum.Font.Gotham
discordButton.TextSize = 14
discordButton.Text = "Join Discord Server"

-- Button functionality: copy link to clipboard
local DISCORD_LINK = "https://discord.gg/SY3zUncE9J"
discordButton.MouseButton1Click:Connect(function()
    setclipboard(DISCORD_LINK)
    game.StarterGui:SetCore("SendNotification", {
        Title = "Nezuko Hub",
        Text = "Discord link copied to clipboard!",
        Duration = 3
    })
end)

return NezukoHub
