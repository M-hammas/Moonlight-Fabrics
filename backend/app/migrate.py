from sqlalchemy import inspect,text

def ensure_columns(engine):
    inspector=inspect(engine)
    additions_by_table={
      'products':{'sku':'VARCHAR(80)','images':'TEXT DEFAULT \'[]\'','sizes':'TEXT DEFAULT \'[]\'','colors':'TEXT DEFAULT \'[]\'','featured':'BOOLEAN DEFAULT FALSE'},
      'orders':{'tracking_number':'VARCHAR(64)','courier':'VARCHAR(120) DEFAULT \'Sidra Fabrics Delivery\''}
    }
    with engine.begin() as conn:
      for table,additions in additions_by_table.items():
        existing={c['name'] for c in inspect(conn).get_columns(table)}
        for name,definition in additions.items():
          if name not in existing:
            conn.execute(text(f'ALTER TABLE {table} ADD COLUMN {name} {definition}'))
