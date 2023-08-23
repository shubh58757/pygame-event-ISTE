while running:
    score=score+1

    player_image_width = player.img.get_width()
    player_image_height = player.img.get_height()
    laser_image_width = player.laser_img.get_width()
    laser_image_height = player.laser_img.get_height()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not player.is_jump:
                if event.key == pygame.K_SPACE:
                    player.is_jump = True
                if event.key == pygame.K_RIGHT:
                    player.shoot()

    if player.is_jump:
        player.jump()

    for laser in player.lasers[:]:
        laser.move(laser_vel)
        laser.draw(screen)

    for enemy in enemies[:]:
        if laser.rect.colliderect(enemy.rect):
            player.lasers.remove(laser)
            enemies.remove(enemy)
            break


    keys = pygame.key.get_pressed()

    # if keys[pygame.K_UP]:
    #     player.shoot()

    speed_increasing_rate += 0.006
    bg_x -= (10 + speed_increasing_rate)

    if bg_x < -bg_width:
        bg_x = 0

    screen.blit(background_image, (bg_x, 0))
    screen.blit(background_image, (bg_x + bg_width, 0))

    player.draw(screen) 

    for laser in player.lasers[:]:
        for enemy in enemies[:]:
            if laser.x + laser_image_width > enemy.x and laser.x < enemy.x + enemy.rect.width:
                if laser.collision(enemy):
                    player.lasers.remove(laser)
                    enemies.remove(enemy)
                    break


    current_time = pygame.time.get_ticks()  

    if current_time - last_enemy_spawn_time >= 2000:
        if random.randint(0, 100) < 2:
            enemy_x = screen_width
            enemy_y = 386
            enemy = Enemy(enemy_x, enemy_y)
            enemies.append(enemy)
            last_enemy_spawn_time = current_time  

    for enemy in enemies:
        enemy.x -= 15
        enemy.draw()
        enemy.run_animation_enemy()

        if enemy.rect.colliderect(player.rect):
            player_lives -= 1
            player.x = 100  
            player.y = 386 
            speed_increasing_rate = 0

            if player_lives <= 0:
                game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
                screen.blit(game_over_text, (screen_width // 2 - 120, screen_height // 2))
                pygame.display.update()
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()

            #enemies.remove(enemy)  # Move this line inside the collision check loop

        if enemy.x + enemy.rect.width < 0:
            enemies.remove(enemy)

    lives_text = font.render(f"Lives: {player_lives}", True, (0, 0, 0))
    screen.blit(lives_text, (screen_width - 120, 10))
    
    score_text= font.render(f"Score:{score}",True,(0,0,0))
    screen.blit(score_text,(20,10))

    player.run_animation_player()
    pygame.display.update()
    clock.tick(30)

pygame.quit()