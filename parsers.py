def parse_eft(fit):
    """Parse an EFT-formatted fit into a dict of:
    {name: str, items: {item: quantity}}

    Example input:
        [Skiff, El'Miner's Skiff]
        Mining Laser Upgrade II
        Mining Laser Upgrade II

        Dread Guristas Kinetic Shield Hardener
        Drone Navigation Computer I
        Multispectrum Shield Hardener II
        Shield Recharger II
        Survey Scanner II

        Modulated Strip Miner II,Kernite Mining Crystal II

        Medium Ice Harvester Accelerator I
        Medium Kinetic Shield Reinforcer I

        Salvage Drone I x3
        Salvage Drone I x5

    Example output:
        {
            'name': "El'Miner's Skiff",
            'items': {
                'Skiff': 1,
                'Mining Laser Upgrade II': 2,
                'Dread Guristas Kinetic Shield Hardener': 1,
                'Drone Navigation Computer I': 1,
                'Multispectrum Shield Hardener II': 1,
                'Shield Recharger II': 1,
                'Survey Scanner II': 1,
                'Medium Ice Harvester Accelerator I': 1,
                'Medium Kinetic Shield Reinforcer I': 1,
                'Salvage Drone I': 8
            }
        }

    :param fit: str EFT-formatted fit
    :return: dict {name: str, items: {item: quantity}}
    """
    if not fit.startswith('['):
        # Not in EFT format
        return None

    fitting = {'items': {}}
    lines = fit.strip().splitlines()

    # [Muninn, Doctrine Muninn]
    hull, name = lines[0].strip('[]').split(', ')
    fitting['name'] = name
    fitting['items'][hull] = 1

    for line in lines[1:]:
        line = line.strip()

        # Skip blank lines and empty slots
        if not line or line.startswith('[Empty'):
            continue

        # line contains a module and charge
        if ',' in line:
            module, charge = line.split(',')
            if module in fitting['items']:
                fitting['items'][module] += 1
            else:
                fitting['items'][module] = 1
            if charge in fitting['items']:
                fitting['items'][charge] += 1
            else:
                fitting['items'][charge] = 1
        else:
            # # item with quantity
            if line.split()[-1].startswith('x'):
                item = ' '.join(line.split()[:-1])
                qty = int(line.split()[-1].strip('x'))
                if item in fitting['items']:
                    fitting['items'][item] += qty
                else:
                    fitting['items'][item] = qty
            else:
                if line in fitting['items']:
                    fitting['items'][line] += 1
                else:
                    fitting['items'][line] = 1
    return fitting
