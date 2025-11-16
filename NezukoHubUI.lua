--// NezukoHub UI Library (Rayfield Copy)

local NezukoHub = {}
NezukoHub.__index = NezukoHub

local UIS = game:GetService("UserInputService")

function NezukoHub:CreateWindow(config)
    local Window = {}

    -- create ScreenGui
    local gui = Instance.new("ScreenGui")
    gui.Name = config.Name or "NezukoHub"
    gui.Parent = game.CoreGui

    -- main frame
    local main = Instance.new("Frame")
    main.Name = "Main"
    main.Parent = gui
    main.Size = UDim2.new(0, 500, 0, 320)
    main.Position = UDim2.new(0.5, -250, 0.5, -160)
    main.BackgroundColor3 = Color3.fromRGB(25,25,25)
    main.Active = true
    main.Draggable = true

    -- title bar
    local title = Instance.new("TextLabel")
    title.Parent = main
    title.Size = UDim2.new(1, 0, 0, 40)
    title.BackgroundColor3 = Color3.fromRGB(32,32,32)
    title.Text = config.Name or "Nezuko Hub"
    title.TextColor3 = Color3.new(1,1,1)
    title.Font = Enum.Font.GothamBold
    title.TextSize = 20

    Window.GUI = gui
    Window.Main = main

    setmetatable(Window, {
        __index = function(_, k)
            return NezukoHub[k]
        end
    })

    return Window
end

function NezukoHub:CreateTab(config)
    local Tab = {}

    local button = Instance.new("TextButton")
    button.Parent = self.Main
    button.Size = UDim2.new(0, 120, 0, 28)
    button.Position = UDim2.new(0, 10, 0, 50)
    button.Text = config.Name
    button.BackgroundColor3 = Color3.fromRGB(40,40,40)
    button.Font = Enum.Font.Gotham
    button.TextColor3 = Color3.new(1,1,1)
    button.TextSize = 14
    button.AutoButtonColor = true

    local page = Instance.new("Frame")
    page.Parent = self.Main
    page.Size = UDim2.new(1, -140, 1, -60)
    page.Position = UDim2.new(0, 135, 0, 50)
    page.BackgroundColor3 = Color3.fromRGB(30,30,30)
    page.Visible = false

    button.MouseButton1Click:Connect(function()
        for _, v in pairs(self.Main:GetChildren()) do
            if v:IsA("Frame") and v.Name == "Page" then
                v.Visible = false
            end
        end
        page.Visible = true
    end)

    Tab.Page = page

    setmetatable(Tab, {
        __index = function(_, k)
            return NezukoHub[k]
        end
    })

    return Tab
end

function NezukoHub:CreateToggle(config)
    local Toggle = {}

    local btn = Instance.new("TextButton")
    btn.Parent = config.Tab.Page
    btn.Size = UDim2.new(1, -20, 0, 32)
    btn.Position = UDim2.new(0, 10, 0, 10 + (#config.Tab.Page:GetChildren() * 36))
    btn.Text = (config.Name or "Toggle")
    btn.Font = Enum.Font.Gotham
    btn.TextSize = 14
    btn.TextColor3 = Color3.new(1,1,1)
    btn.BackgroundColor3 = Color3.fromRGB(45,45,45)

    local state = false

    btn.MouseButton1Click:Connect(function()
        state = not state

        if config.Callback then
            pcall(config.Callback, state)
        end

        btn.BackgroundColor3 = state and Color3.fromRGB(0, 170, 0) or Color3.fromRGB(45,45,45)
    end)

    return Toggle
end

return NezukoHub
